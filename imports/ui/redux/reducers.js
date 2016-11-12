const initialState = {
  myShows: [],
  topShows: [],
};

const reducers = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_MY_SHOWS':
      return Object.assign({}, state, {
        myShows: action.shows,
      });
    case 'GET_TOP_SHOWS':
      return Object.assign({}, state, {
        topShows: action.shows,
      });
    default:
      return state;
  }
};

export default reducers;
