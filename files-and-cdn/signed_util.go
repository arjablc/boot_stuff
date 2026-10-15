package main

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/bootdotdev/learn-file-storage-s3-golang-starter/internal/database"
)

func (cfg *apiConfig) dbVideoToSignedVideoArchive(video database.Video) (database.Video, error) {
	if video.VideoURL == nil {
		return video, nil
	}
	splits := strings.Split(*video.VideoURL, ", ")
	fmt.Printf("====================\nVideo URL(db saved)\n%s\n=====================", *video.VideoURL)
	if len(splits) != 2 {
		return video, errors.New("Invalid video URL")
	}
	bucket, key := splits[0], splits[1]
	presignedUrl, err := generatePresignedURL(*cfg.s3Client, bucket, key, time.Minute*30)
	if err != nil {
		return video, err
	}
	video.VideoURL = &presignedUrl
	return video, nil
}

func generatePresignedURL(s3Client s3.Client, bucket, key string, expireTime time.Duration) (string, error) {
	presignClient := s3.NewPresignClient(&s3Client)

	getInputParms := s3.GetObjectInput{
		Bucket: &bucket,
		Key:    &key,
	}

	presignGet, err := presignClient.PresignGetObject(context.TODO(), &getInputParms, s3.WithPresignExpires(expireTime))
	if err != nil {
		return "", err
	}

	return presignGet.URL, nil

}
