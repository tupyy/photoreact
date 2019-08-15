/**
 * Create a bare bone XHR object for make POST requests
 * @param url url request
 * @param resolve resolve promise callback
 * @param reject reject promise callback
 * @return {XMLHttpRequest}
 */
export function postXHRObject(url, resolve, reject) {
    return xhrObject("POST", url, resolve, reject);
}

/**
 * Create a bare bone XHR object for make GET requests
 * @param url url request
 * @param resolve resolve promise callback
 * @param reject reject promise callback
 * @return {XMLHttpRequest}
 */
export function getXHRObject(url, resolve, reject) {
    return xhrObject('GET', url, resolve, reject);
}

const xhrObject = function(method, url, resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            resolve(xhr.responseText);
        } else if (xhr.status > 400) {
            reject({
                'reason': xhr.statusText,
                'status': xhr.status
            });
        }
    };
    return xhr;
};
