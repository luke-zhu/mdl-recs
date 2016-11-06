const initialState = {
  myShows: [],
};

const reducers = (state = initialState, action) => {
  switch (action.type) {
    case 'GET_MY_SHOWS':
      return Object.assign({}, state, {
        myShows: action.shows,
      });
    default:
      return state;
  }
};

export default reducers;
