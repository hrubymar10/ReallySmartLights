package main

import (
	"fmt"
	"github.com/hrubymar10/ReallySmartLights/config"
	"github.com/hrubymar10/ReallySmartLights/tradfri"
	"log"
	"math/rand"
	"time"
)

func main() {
	err := config.LoadConfig()
	if err != nil {
		fmt.Println("An unknown error occurred:")
		log.Fatal(err)
	}

	if config.Config.GatewayIP == "" {
		//TODO: Gateway IP Init
	}

	if config.Config.FactoryPSK == "" {
		//TODO: FactoryPSK Init
	}

	if config.Config.PSK == "" {
		performTokenExchange()
	}

	for true {
		for _, bulb := range config.Config.Bulbs {
			fmt.Println(bulb)
		}
		fmt.Println()
		time.Sleep(1 * time.Second)
	}
}

func performTokenExchange() {
	if len(config.Config.ClientID) < 1 {
		config.Config.ClientID = RandStringBytes(8)
	}

	if len(config.Config.FactoryPSK) < 10 {
		log.Fatal("Please enter valid factoryPSK")
	}

	done := make(chan bool)
	defer func() { done <- true }()
	go func() {
		select {
		case <-time.After(time.Second * 5):
			fmt.Println("Performing Token Exchange...")
			fmt.Println("(Please note that the key exchange may appear to be stuck at \"Connecting to peer at\" if the PSK from the bottom of your Gateway is not entered correctly.)")
		case <-done:
		}
	}()

	// Note that we hard-code "Client_identity" here before creating the DTLS client,
	// required when performing token exchange
	dtlsClient := tradfri.NewTradfriClient(config.Config.GatewayIP + ":5684", "Client_identity", config.Config.FactoryPSK)

	authToken, err := dtlsClient.AuthExchange(config.Config.ClientID)
	if err != nil {
		log.Fatal(err.Error())
	}
	config.Config.PSK = authToken.Token

	err = config.SaveConfig()
	if err != nil {
		fmt.Println("An unknown error occurred:")
		log.Fatal(err)
	}

	fmt.Println("Your configuration has been written to config.json!")
}

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func RandStringBytes(n int) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = letterBytes[rand.Intn(len(letterBytes))]
	}
	return string(b)
}