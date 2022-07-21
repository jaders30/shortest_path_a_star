// get Data
const getData =  async (nameRoute, errorMsg) => {
    return await fetch(nameRoute)
            .then(res => res.json())
            .catch(function (error) {
                console.warn(errorMsg, error);
            });
}

// Send Data
const sendData = async (nameRoute, data, errorMsg) => {

    return await fetch(nameRoute, {
            method: 'POST',
            body: JSON.stringify(data),
            mode: 'cors',
           
            headers: { 
                'Content-type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
             }
    }).then((response) => {
    
        return  (!response.ok) ? Promise.reject(response) : response.json();
            
    }).then((data) => {
        return data; 
        
    }).catch((error) => {
        console.warn(errorMsg, error);
    });
}