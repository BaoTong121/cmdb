import axios from "axios"


export default class IpService {
    getip() {
        axios.get('/api/ip')
        .then(function (response) {
          // handle success
          console.log(response);
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        });
    }
    
}