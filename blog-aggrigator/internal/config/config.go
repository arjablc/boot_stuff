package config

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
)

const (
	configFilename = ".gatorconfig.json"
)

type Config struct {
	DbUrl           string `json:"db_url"`
	CurrentUsername string `json:"current_user_name"`
}

func (C *Config) SetUser(userName string) error {
	if userName == "" {
		return errors.New("No username provided")
	}
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return errors.New("Failed to get user Home directory")
	}
	finalPath := filepath.Join(homeDir, configFilename)
	C.CurrentUsername = userName
	data, err := json.Marshal(C)
	if err != nil {
		panic(err)
	}
	err = os.WriteFile(finalPath, data, 0644)
	if err != nil {
		return err
	}
	return nil

}

func Read() (*Config, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return nil, errors.New("Failed to get user Home directory")
	}
	finalPath := filepath.Join(homeDir, configFilename)
	data, err := os.ReadFile(finalPath)
	if err != nil {
		return nil, errors.New("Failed to read config file")
	}
	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return nil, errors.New("Failed to unmarshal, invalid config file")
	}
	return &config, nil

}
