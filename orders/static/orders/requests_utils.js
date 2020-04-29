export function get(url, params={}) {
  // Return a new promise.
  return new Promise(function(resolve, reject) {
    const req = new XMLHttpRequest();
    const url_params = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => url_params.append(key, val));
    //console.log(url_params.toString());
    req.open('GET', `${url}?${url_params.toString()}`);
    console.log(req);

    req.onload = function() {
      // This is called even on 404 etc
      // so check the status
      if (req.status == 200) {
        // Resolve the promise with the response text
        resolve(req.response);
      }
      else {
        // Otherwise reject with the status text
        // which will hopefully be a meaningful error
        reject(Error(req.statusText));
      }
    };

    // Handle network errors
    req.onerror = function() {
      reject(Error("Network Error"));
    };

    // Make the request
    req.send();
  });
}

export function getJSON(url, params={}) {
  return get(url, params).then(JSON.parse);
}


export function post(url, postData={}) {
	return new Promise((resolve, reject) => {
		const req = new XMLHttpRequest();
		req.open('POST', url)
		const data = new FormData();
		Object.entries(postData).forEach(([key, val]) => data.append(key, val));

		req.onload = () => {
			if (req.status == 200) {
				resolve(req.response);
			} else {
				reject(Error(req.statusText));
			}
		}
		// Handle network errors
	    req.onerror = function() {
	      reject(Error("Network Error"));
	    };

	    // Make the request
	    req.send(data);
	});
}

export function postJSON(url, postData={}) {
	return post(url, postData).then(JSON.parse);
}