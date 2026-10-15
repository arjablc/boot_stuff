package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"mime"
	"net/http"
	"os"
	"path/filepath"
	"slices"
	"strings"

	"github.com/bootdotdev/learn-file-storage-s3-golang-starter/internal/auth"
	"github.com/google/uuid"
)

var allowedTypes []string = []string{"image/jpeg", "image/png"}

func (cfg *apiConfig) handlerUploadThumbnail(w http.ResponseWriter, r *http.Request) {

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

	fmt.Println("uploading thumbnail for video", videoID, "by user", userID)

	const maxMemory int64 = 10 << 20
	r.ParseMultipartForm(int64(maxMemory))
	file, fileHeader, err := r.FormFile("thumbnail")
	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}
	contentType := fileHeader.Header.Get("Content-Type")

	mediaType, _, err := mime.ParseMediaType(contentType)
	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}
	if !slices.Contains(allowedTypes, mediaType) {
		respondWithError(w, http.StatusBadRequest, "Bad file type", err)
		return
	}

	// NOTE: This will read the file to exhaustion
	//leading to zero bytes being copied when using io.copy
	// fileData, err := io.ReadAll(file)
	videoMeta, err := cfg.db.GetVideo(videoID)

	if err != nil {
		respondWithError(w, 404, "Video Metadata wan't found", err)
		return
	}
	if videoMeta.UserID != userID {
		respondWithError(w, http.StatusUnauthorized, "Unauthorized", err)
		return
	}
	buff := make([]byte, 32)
	_, err = rand.Read(buff)
	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}
	fName := base64.RawURLEncoding.EncodeToString(buff)
	fileExt := fmt.Sprintf(".%s", strings.Split(mediaType, "/")[1])
	fileName := fName + fileExt
	path := filepath.Join(cfg.assetsRoot, fileName)
	createdFile, err := os.Create(path)

	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}
	defer createdFile.Close()

	_, err = io.Copy(createdFile, file)
	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}

	port := os.Getenv("PORT")
	thumbUrl := fmt.Sprintf("http://localhost:%s/assets/%s", port, fileName)
	videoMeta.ThumbnailURL = &thumbUrl
	err = cfg.db.UpdateVideo(videoMeta)
	if err != nil {
		respondWithError(w, 500, "Internal Server Error", err)
		return
	}
	updatedVideo, err := cfg.db.GetVideo(videoID)
	if err != nil {
		respondWithError(w, 404, "Video Metadata wan't found", err)
		return
	}

	respondWithJSON(w, http.StatusOK, updatedVideo)
}
