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
	"strings"

	"github.com/gorilla/mux"
)

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

func NewRouter() *mux.Router {
	router := mux.NewRouter().StrictSlash(true)
	for _, route := range routes {
		var handler http.Handler
		handler = route.HandlerFunc
		handler = Logger(handler, route.Name)

		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}

	return router
}

func Index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World!")
}

var routes = Routes{
	Route{
		"Index",
		"GET",
		"/",
		Index,
	},

	Route{
		"DataFileIdGet",
		strings.ToUpper("Get"),
		"/data/{fileId}",
		DataFileIdGet,
	},

	Route{
		"DataFileIdPost",
		strings.ToUpper("Post"),
		"/data/{fileId}",
		DataFileIdPost,
	},

	Route{
		"DataProjectProjectNoPost",
		strings.ToUpper("Post"),
		"/data/project/{projectNo}",
		DataProjectProjectNoPost,
	},

	Route{
		"MessagesGet",
		strings.ToUpper("Get"),
		"/messages",
		MessagesGet,
	},

	Route{
		"MessagesIdPatch",
		strings.ToUpper("Patch"),
		"/messages/{id}",
		MessagesIdPatch,
	},

	Route{
		"MessagesPatch",
		strings.ToUpper("Patch"),
		"/messages",
		MessagesPatch,
	},

	Route{
		"ProjectsProjectNoConfirmPost",
		strings.ToUpper("Post"),
		"/projects/{projectNo}/confirm",
		ProjectsProjectNoConfirmPost,
	},

	// Route{
	// 	"TestMarkDeliveryReadyPost",
	// 	strings.ToUpper("Post"),
	// 	"/test/mark-delivery-ready",
	// 	TestMarkDeliveryReadyPost,
	// },

	// Route{
	// 	"TestMoveReceivedTransferFilePost",
	// 	strings.ToUpper("Post"),
	// 	"/test/move-received-transfer-file",
	// 	TestMoveReceivedTransferFilePost,
	// },

	// Route{
	// 	"TestRecallDeliveryPost",
	// 	strings.ToUpper("Post"),
	// 	"/test/recall-delivery",
	// 	TestRecallDeliveryPost,
	// },

	// Route{
	// 	"TestSynchronizePost",
	// 	strings.ToUpper("Post"),
	// 	"/test/synchronize",
	// 	TestSynchronizePost,
	// },

	Route{
		"UserAccessesAccessIdentifierPatch",
		strings.ToUpper("Patch"),
		"/user-accesses/{accessIdentifier}",
		UserAccessesAccessIdentifierPatch,
	},

	Route{
		"UserAccessesPost",
		strings.ToUpper("Post"),
		"/user-accesses",
		UserAccessesPost,
	},
}
