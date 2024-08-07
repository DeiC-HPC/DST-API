/*
 * Danish Data Portal - HPC API
 *
 * A Web API for HPC centers to communicate with the Danish Data Portal to manage access and data transfers
 *
 * API version: v1
 * Generated by: Swagger Codegen (https://github.com/swagger-api/swagger-codegen.git)
 */
package swagger

import (
	"fmt"
	"net/http"
	"encoding/json"
	"strings"
	"strconv"
)

var MESSAGELISTORDERING []CreateMessage = []CreateMessage{
	generateCreateProject("1337"),
	generateCreateProjectAccess("1337","Test"),
	generateDisableProjectAccess("Test"),
	generateEnableProjectAccess("Test"),
	generateResetPassword("Test"),
	generateDataDeliveryReady(
		"DeliveryId",
		"1337",
		"File",
		"1",
		"0"),
	generateDeleteDataFile("File"),
	generateReturnDataFile("File"),
	generateDeleteProjectAccess("Test"),
	generateDeleteProject("1337")}

func getMessages() []Data{
	for i := 0; i < len(MESSAGELISTORDERING); i++ {
		updateMessageQueue(MESSAGELISTORDERING[i])
	}
	data := generateMessages()
	return data
}

func MessagesGet(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(getMessages())
	fmt.Println(confirmQueue)
}

func MessagesIdPatch(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	messageIdString := strings.Split(r.RequestURI, "/messages/")[1]
	messageId, err := strconv.Atoi(messageIdString)
	if err != nil {
		fmt.Println("Error converting the following messageId to an integer: ", err)
	}

	//Look only for the first message in the confirmQueue
	if(confirmQueue != nil && confirmQueue[0] == messageId){
		w.WriteHeader(http.StatusOK)
		confirmQueue = confirmQueue[1:]
	} else {
		w.WriteHeader(http.StatusNotFound)
	}
	fmt.Println(confirmQueue)
}

func MessagesPatch(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusNotImplemented)
}
