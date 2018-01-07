import {
  DISPLAY_FAILURE_ICON, DISPLAY_LOADING_ICON, RECEIVE_SHOWS,
  SELECT_SHOW,
} from './actions';

const initialState = {
  loading: false,
  failed: false,
  shows: [],
  selectedShow: null,
};

const reducers = (state = initialState, action) => {
  switch (action.type) {
    case DISPLAY_LOADING_ICON:
      return Object.assign({}, state, {
        loading: true,
        failed: false,
      });
    case DISPLAY_FAILURE_ICON:
      return Object.assign({}, state, {
        loading: false,
        failed: true,
      });
    case RECEIVE_SHOWS:
      return Object.assign({}, state, {
        shows: action.hits,
        selectedShow: action.hits[0],
      });
    case SELECT_SHOW:
      // TODO
      return Object.assign({}, state, {
        selectedShow: {},
      });
    default:
      return state;
  }
};

export default reducers;
