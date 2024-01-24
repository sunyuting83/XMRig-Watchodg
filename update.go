package main

import (
	"archive/zip"
	"errors"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/lxn/walk"
	. "github.com/lxn/walk/declarative"
	"github.com/lxn/win"
	"golang.org/x/text/encoding/simplifiedchinese"
)

type Charset string

const (
	UTF8    = Charset("UTF-8")
	GB18030 = Charset("GB18030")
)

func ConvertByte2String(byte []byte, charset Charset) string {
	var str string
	switch charset {
	case GB18030:
		var decodeBytes, _ = simplifiedchinese.GB18030.NewDecoder().Bytes(byte)
		str = string(decodeBytes)
	case UTF8:
		fallthrough
	default:
		str = string(byte)
	}
	return str
}

func RunCommandWithRaw() (string, error) {
	cmdExec := exec.Command("tasklist", "/fo", "csv", "/nh")
	cmd := exec.Command("cmd.exe")
	cmd.SysProcAttr = &syscall.SysProcAttr{
		CmdLine: fmt.Sprintf(`/c %s`, cmdExec), HideWindow: true}
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return ConvertByte2String(output, "GB18030"), nil
}

func RunExec(appname string) {
	cmd := exec.Command("cmd.exe", "/c", appname)
	cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
	cmd.Start()
}

func getPIDByProcessName(output, processName string) (int, error) {
	lines := strings.Split(output, "\n")
	for _, line := range lines {
		fields := strings.Split(line, ",")
		if len(fields) >= 2 {
			name := strings.Trim(fields[0], "\"")
			pid := strings.TrimSpace(fields[1])
			pid = strings.Trim(pid, "\"")
			if name == processName {
				pidInt, _ := strconv.Atoi(pid)
				return pidInt, nil
			}
		}
	}

	return 0, fmt.Errorf("cant find %s", processName)
}

func GetSystemRoot() string {
	windowsDir := os.Getenv("SystemRoot")
	// fmt.Println(windowsDir)
	if windowsDir == "" {
		windowsDir = "C:\\Windows"
	}
	return windowsDir
}

func GetCurrentPath() (string, error) {
	path, err := os.Executable()
	if err != nil {
		return "", err
	}
	dir := filepath.Dir(path)
	return dir, nil
}

func Unzip(source, destination string) error {
	zipReader, err := zip.OpenReader(source)
	if err != nil {
		return err
	}
	defer zipReader.Close()

	for _, file := range zipReader.File {
		filePath := filepath.Join(destination, file.Name)

		if file.FileInfo().IsDir() {
			os.MkdirAll(filePath, file.Mode())
			continue
		}

		fileDir := filepath.Dir(filePath)
		err := os.MkdirAll(fileDir, 0755)
		if err != nil {
			return err
		}

		writer, err := os.Create(filePath)
		if err != nil {
			return err
		}
		defer writer.Close()

		reader, err := file.Open()
		if err != nil {
			return err
		}
		defer reader.Close()

		_, err = io.Copy(writer, reader)
		if err != nil {
			return err
		}
	}
	return nil
}

func RunCommand(cmdExec string) (k string, err error) {
	cmd := exec.Command("cmd.exe")
	cmd.SysProcAttr = &syscall.SysProcAttr{
		CmdLine: fmt.Sprintf(`/c %s`, cmdExec), HideWindow: true}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		// fmt.Println(err)
		return "", err
	}
	defer stdout.Close()

	stderr, err := cmd.StderrPipe()
	if err != nil {
		// fmt.Println(err)
		return "", err
	}
	defer stderr.Close()

	if err := cmd.Start(); err != nil {
		// fmt.Println(err)
		return "", err
	}

	bytesErr, err := io.ReadAll(stderr)
	if err != nil {
		// fmt.Println(err)
		return "", err
	}

	if len(bytesErr) != 0 {
		return "", errors.New("0")

	}

	bytes, err := io.ReadAll(stdout)
	if err != nil {
		// fmt.Println(err)
		return "", err
	}

	if err := cmd.Wait(); err != nil {
		// fmt.Println(err)
		return "", err
	}
	return string(bytes), nil
}

func IsExist(path string) bool {
	// 判断文件是否存在
	_, err := os.Stat(path)
	return err == nil || os.IsExist(err)
}

func getWatchdogPid(appName string) (int, error) {
	var lines string
	var err error
	var pid int = 0
	SystemRoot := GetSystemRoot()
	WMIC_path := strings.Join([]string{SystemRoot, "System32", "wbem"}, `\`)
	// fmt.Println(WMIC_path)
	if IsExist(WMIC_path) {
		// fmt.Println("here")
		WMIC := strings.Join([]string{WMIC_path, "wmic"}, `\`)
		command := strings.Join([]string{WMIC, ` process where "name like '`, appName, `'" get ProcessId`}, "")
		// fmt.Println(command)
		lines, _ = RunCommand(command)
		// fmt.Println(lines)
	} else {
		lines, err = RunCommandWithRaw()
		if err != nil {
			// fmt.Println(err.Error())
			// fmt.Println("发生错误")
			return 0, err
		}
	}
	if len(lines) > 0 && strings.Contains(lines, "ProcessId") {
		lines_list := strings.Split(lines, "\n")
		pidStr := lines_list[1]
		pidStr = strings.TrimSpace(pidStr)
		pidStr = strings.Trim(pidStr, "\r")
		// fmt.Println(pidStr)
		pid, _ = strconv.Atoi(pidStr)
	} else {
		if len(lines) != 0 {
			pid, err = getPIDByProcessName(lines, appName)
			if err != nil {
				if !strings.Contains(err.Error(), "cant find") {
					return 0, err
				}
			}
		}
	}
	return pid, nil
}

func GetAllFile(pathname string) (string, string) {
	// 获取文件目录下所有文件
	a := ""
	b := ""
	rd, err := os.ReadDir(pathname)
	if err != nil {
		// fmt.Println("read dir fail:", err)
		return "", ""
	}
	for _, fi := range rd {
		if fi.IsDir() {
			// fmt.Printf("[%s]\n", pathname+"/"+fi.Name())
			GetAllFile(strings.Join([]string{pathname, fi.Name(), `\`}, ""))
		} else {
			fileSuffix := path.Ext(fi.Name())
			if fileSuffix == ".exe" || fileSuffix == ".zip" {
				a = strings.Join([]string{pathname, fi.Name()}, `\`)
				b = fileSuffix
			}
		}
	}
	return a, b
}

type LogView struct {
	walk.TextEdit
}

func NewLogView(parent walk.Container) (*LogView, error) {
	e, err := walk.NewTextEditWithStyle(parent, win.WS_VSCROLL)
	if err != nil {
		return nil, err
	}
	lv := &LogView{*e}
	lv.SetReadOnly(true)
	return lv, nil
}

func (lv *LogView) PostAppendText(value string) {
	lv.AppendText(value)
}

func (lv *LogView) Write(p []byte) (int, error) {
	lv.PostAppendText(string(p))
	return len(p), nil
}

func main() {
	var appName string
	var xmrName string
	flag.StringVar(&appName, "appname", "XMRigWatchdog.exe", "Program Name")
	flag.StringVar(&xmrName, "xmrname", "xmrig.exe", "XMRig Name")
	flag.Parse()

	CurrentPath, _ := GetCurrentPath()
	ExecPath := strings.Join([]string{CurrentPath, appName}, "\\")
	internalPath := strings.Join([]string{CurrentPath, "_internal"}, "\\")
	TmpPath := strings.Join([]string{CurrentPath, "tmp"}, "\\")
	var mw *walk.MainWindow
	// fmt.Println(internalPath)
	if err := (MainWindow{
		AssignTo: &mw,
		Title:    "Update",
		MinSize:  Size{320, 240},
		Size:     Size{320, 240},
		Layout:   VBox{MarginsZero: true},
	}.Create()); err != nil {
		log.Fatal(err)
	}

	lv, err := NewLogView(mw)
	if err != nil {
		log.Fatal(err)
	}

	lv.PostAppendText("正在准备更新……\r\n")
	log.SetOutput(lv)
	go func() {
		pid, err := getWatchdogPid(appName)
		if err != nil {
			log.Println("发生错误,请手动更新")
			return
		}
		if pid != 0 {
			pidStr := strconv.Itoa(pid)
			process := strings.Join([]string{"taskkill /f /pid", pidStr}, " ")
			RunCommand(process)
		}

		xmr_pid, err := getWatchdogPid(xmrName)
		if err != nil {
			log.Println("发生错误,请手动更新")
			return
		}
		if xmr_pid != 0 {
			pidStr := strconv.Itoa(xmr_pid)
			process := strings.Join([]string{"taskkill /f /pid", pidStr}, " ")
			RunCommand(process)
		}
		log.Println("正在检测更新文件是否存在")
		TempFile, fileSuffix := GetAllFile(TmpPath)
		// log.Println(internalPath)
		if TempFile != "" {
			log.Println("更新文件存在, 升级中……\r\n")
			if fileSuffix == ".exe" {
				log.Println("正在删除旧文件……\r\n")
				os.Remove(ExecPath)
				time.Sleep(1000 * time.Millisecond)
				os.Remove(internalPath)
				time.Sleep(1000 * time.Millisecond)
				log.Println("正在拷贝新文件……\r\n")
				os.Rename(TempFile, ExecPath)
				time.Sleep(1000 * time.Millisecond)
				log.Println("更新成功,正在退出……\r\n")
				log.Println("启动主程序")
				time.Sleep(1000 * time.Millisecond)
				RunExec(ExecPath)
				time.Sleep(1000 * time.Millisecond)
				os.Exit(3)
			}
			log.Println("正在删除旧文件……\r\n")
			os.Remove(ExecPath)
			os.Remove(internalPath)
			log.Println("zip文件解压中……\r\n")
			Unzip(TempFile, CurrentPath)
			log.Println("zip文件解压成功……\r\n")
			time.Sleep(1000 * time.Millisecond)
			log.Println("正在删除zip文件……\r\n")
			os.Remove(TempFile)
			time.Sleep(1000 * time.Millisecond)
			log.Println("启动主程序\r\n")
			go RunExec(ExecPath)
			time.Sleep(1000 * time.Millisecond)
			os.Exit(3)
		}
		log.Println("更新文件不存在,请手动更新")
	}()

	mw.Run()
}
