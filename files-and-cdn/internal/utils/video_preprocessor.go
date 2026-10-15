package utils

import "os/exec"

func ProcessVideoForFasterStart(filePath string) (string, error) {
	outFile := filePath + ".processed"
	cmd := exec.Command("ffmpeg", "-i", filePath, "-c", "copy", "-movflags", "faststart", "-f", "mp4", outFile)

	err := cmd.Run()
	if err != nil {
		return "", err
	}
	return outFile, nil
}
