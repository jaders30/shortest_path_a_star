const uri = '/api';

const routeTo = (sub) =>  (uri + sub);

const sendAllPossibleRoutes  = async (data) => {
    const theRoute = routeTo('/possibleroutes');
    const erMsg = "Something went wrong sending routes."
    return await sendData(theRoute, data, erMsg);
}


const getRecommendedRoutes  = async () => {
    const theRoute = routeTo('/recommendedroutes');
    const erMsg = "Something went wrong getting recommended routes."
    return await getData(theRoute, erMsg);
}




