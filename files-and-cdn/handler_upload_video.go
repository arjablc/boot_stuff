package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"mime"
	"net/http"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/bootdotdev/learn-file-storage-s3-golang-starter/internal/auth"
	"github.com/bootdotdev/learn-file-storage-s3-golang-starter/internal/utils"
	"github.com/google/uuid"
)

func (cfg *apiConfig) handlerUploadVideo(w http.ResponseWriter, r *http.Request) {
	const maxSize int64 = 1 << 30
	r.Body = http.MaxBytesReader(w, r.Body, maxSize)
	defer r.Body.Close()

	videoIDString := r.PathValue("videoID")
	videoID, err := uuid.Parse(videoIDString)
	if err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid ID", err)
		return
	}
	token, err := auth.GetBearerToken(r.Header)
	if err != nil {
		respondWithError(w, http.StatusUnauthorized, "Couldn't find JWT", err)
		return
	}
	userID, err := auth.ValidateJWT(token, cfg.jwtSecret)
	if err != nil {
		respondWithError(w, http.StatusUnauthorized, "Couldn't validate JWT", err)
		return
	}
	video, err := cfg.db.GetVideo(videoID)
	if err != nil {
		respondWithError(w, http.StatusNotFound, "Video Metadata wan't found", err)
		return
	}
	if video.UserID != userID {
		respondWithError(w, http.StatusUnauthorized, "Unauthorized", err)
		return
	}
	reqFile, fileHeaders, err := r.FormFile("video")
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Can't parse file", err)
		return
	}
	defer reqFile.Close()
	contentType := fileHeaders.Header.Get("Content-Type")
	mediaType, _, err := mime.ParseMediaType(contentType)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Can't parse media type", err)
		return
	}
	if mediaType != "video/mp4" {
		respondWithError(w, http.StatusBadRequest, "Invalid file type", err)
		return
	}
	tempVdoFile, err := os.CreateTemp("", "tubely-upload.mp4")
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Internal Server Error", err)
		return
	}
	defer os.Remove(tempVdoFile.Name())
	defer tempVdoFile.Close()
	_, err = io.Copy(tempVdoFile, reqFile)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Internal Server Error", err)
		return
	}
	// This is done to reset after the code has already read the entire file
	tempVdoFile.Seek(0, io.SeekStart)
	buff := make([]byte, 32)
	_, err = rand.Read(buff)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Internal Server Error", err)
		return
	}
	aspectRatio, err := utils.GetVideoAspectRatio(tempVdoFile.Name())
	var videoOrientation string
	switch aspectRatio {
	case "16:9":
		videoOrientation = "landscape"
	case "9:16":
		videoOrientation = "portrait"
	default:
		videoOrientation = "other"
	}
	//NOTE: Preprocessing
	processedFilePath, err := utils.ProcessVideoForFasterStart(tempVdoFile.Name())
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Internal Server Error", err)
		return
	}
	processedFile, err := os.Open(processedFilePath)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Internal Server Error", err)
		return
	}
	defer processedFile.Close()

	fName := base64.RawURLEncoding.EncodeToString(buff)
	fileExt := fmt.Sprintf(".%s", strings.Split(mediaType, "/")[1])
	fileName := fName + fileExt
	keyWithPref := fmt.Sprintf("%s/%s", videoOrientation, fileName)

	// Lets use signed urls for showing
	// we still use normal put

	inputOpts := s3.PutObjectInput{
		Bucket:      &cfg.s3Bucket,
		Key:         &keyWithPref,
		ContentType: &mediaType,
		Body:        processedFile,
	}
	_, err = cfg.s3Client.PutObject(r.Context(), &inputOpts)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Failed to put object", err)
		return
	}
	videoUrl := fmt.Sprintf("https://%s/%s", cfg.s3CfDistribution, keyWithPref)
	video.VideoURL = &videoUrl
	err = cfg.db.UpdateVideo(video)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Update Failure", err)
		return
	}
	respondWithJSON(w, http.StatusOK, video)

}
