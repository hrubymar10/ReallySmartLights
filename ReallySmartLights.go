package main

import (
	"fmt"
	"github.com/hrubymar10/ReallySmartLights/config"
	"log"
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
}