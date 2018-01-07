export const DISPLAY_LOADING_ICON = 'DISPLAY_LAODING_ICON';

export function displayLoadingIcon() {
  return {
    type: DISPLAY_LOADING_ICON,
  };
}

export const DISPLAY_FAILURE_ICON = 'DISPLAY_FAILURE_ICON';

/*
 * Failed to receive shows (due to internet failure etc.)
 */
export function displayFailureIcon() {
  return {
    type: DISPLAY_FAILURE_ICON,
  };
}

/*
 * Search the Elasticsearch index for a title and the dispatches
 * the RECEIVE_SHOWS action.
 */
export function searchForShow(title) {
  return (dispatch) => {
    // TODO: Get a static IP for the Elasticsearch VM
    fetch('http://35.227.63.208:9200', {method: 'OPTIONS'}).then((response) => {
      const url = `http://35.227.63.208:9200/
      show/_search?q=main_title:${title}`;
      return fetch(url);
    }).then((response) => {
      return response.json();
    }).then((json) => {
      console.log(json);
      dispatch(receiveShows(json.hits.hits));
    }).catch((reason) => {
      console.log(reason);
      dispatch(displayFailureIcon());
    });
  };
}

export const RECEIVE_SHOWS = 'RECEIVE_SHOWS';

export function receiveShows(hits) {
  return {
    type: RECEIVE_SHOWS,
    hits,
  };
}

export const SELECT_SHOW = 'SELECT_SHOW';

/*
 * Marks the show with the title as the foreground show.
 */
export function selectShow(title) {
  return {
    type: SELECT_SHOW,
    title,
  };
}

export function loadHighlights(title) {
  return (dispatch) => {
    fetch('http://35.227.63.208:9200', {method: 'OPTIONS'}).then((response) => {
      const url = `http://35.227.63.208:9200/
      show/_search?q=main_title:${title}`;
      return fetch(url);
    }).then((response) => {
      return response.json();
    })
  }
}