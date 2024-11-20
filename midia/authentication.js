function authenticate(helper, paramsValues, credentials) {
        print("Authenticating via JavaScript script...");
        // Make sure any Java classes used explicitly are imported
        var HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader")
        var HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader")
        var URI = Java.type("org.apache.commons.httpclient.URI")
        
        // Prepare the login request details
        var requestUri = new URI(paramsValues.get("Target URL"), false);
        var requestMethod = HttpRequestHeader.POST;
	
	    // Build the request body using the credentials values
        var extraPostData = paramsValues.get("Extra POST data");
        var requestBody = paramsValues.get("Username field") + "=" + encodeURIComponent(credentials.getParam("Username"));
        requestBody+= "&" + paramsValues.get("Password field") + "=" + encodeURIComponent(credentials.getParam("Password"));
        
        if(extraPostData.trim().length() > 0)
            requestBody += "&" + extraPostData.trim();

    	// Build the actual message to be sent
        print("Sending " + requestMethod + " request to " + requestUri + " with body: " + requestBody);
        var msg = helper.prepareMessage();
        msg.setRequestHeader(new HttpRequestHeader(requestMethod, requestUri, HttpHeader.HTTP10));
        msg.setRequestBody(requestBody);
        msg.getRequestHeader().setContentLength(msg.getRequestBody().length());

    	// Send the authentication message and return it
        helper.sendAndReceive(msg);
        print("Received response status code: " + msg.getResponseHeader().getStatusCode());

	    return msg;
    }
    
    function getRequiredParamsNames(){
        return ["Target URL", "Username field", "Password field"];
    }

    function getOptionalParamsNames(){
        return ["Extra POST data"];
    }

    function getCredentialsParamsNames(){
        return ["Username", "Password"];
    }
  