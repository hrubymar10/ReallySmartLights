package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
)

var Config ConfigStruct
var configFilePath string

type ConfigStruct struct {
	ClientID     string   `json:"client_id"`
	GatewayIP    string   `json:"gateway_ip"`
	FactoryPSK   string   `json:"factory_psk"`
	PSK          string   `json:"psk"`
	Bulbs        []int    `json:"bulbs"`
}

func InitEmptyConfig() error {
	Config = ConfigStruct{}
	return SaveConfig()
}

func LoadConfig() error {
	_, err := os.Stat(getConfigFilePath())
	if err != nil {
		if os.IsNotExist(err) {
			err = InitEmptyConfig()
			if err != nil {
				return err
			}
		} else {
			return err
		}
	}

	file, err := ioutil.ReadFile(getConfigFilePath())
	if err != nil {
		fmt.Println("An unknown error occurred:")
		log.Fatal(err)
	}

	return json.Unmarshal([]byte(file), &Config)
}

func SaveConfig() error {
	file, _ := json.MarshalIndent(Config, "", "	")

	err := ioutil.WriteFile(getConfigFilePath(), file, 0644)

	return err
}

func getConfigFilePath() string {
	if configFilePath == "" {
		dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
		if err != nil {
			fmt.Println("An unknown error occurred:")
			log.Fatal(err)
		}

		configFilePath = dir + string(filepath.Separator) + "config.json"
	}

	return configFilePath
}