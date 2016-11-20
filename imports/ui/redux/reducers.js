const initialState = {
  loading: false,
  myShows: [],
  topShows: [],
  similarShows: [],
};

const reducers = (state = initialState, action) => {
  switch (action.type) {
    case 'SHOW_LOADING':
      return Object.assign({}, state, {
        loading: true,
      });
    case 'GET_MY_SHOWS':
      return Object.assign({}, state, {
        myShows: action.shows,
      });
    case 'GET_TOP_SHOWS':
      return Object.assign({}, state, {
        topShows: action.shows,
      });
    case 'GET_SIMILAR_SHOWS':
      return Object.assign({}, state, {
        similarShows: action.shows,
      });
    default:
      return state;
  }
};

export default reducers;
