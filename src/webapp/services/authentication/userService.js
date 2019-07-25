export default function authenticationService(username, password) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (username === 'demo' && password === 'demo') {
                resolve(
                    {
                        'token': 'token',
                        'id': 'id',
                        'username':username
                    })
            } else {
                reject({'reason': 'wrong password'});
            }
        }, 2000);
    });
}
