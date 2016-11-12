export const getMyShows = shows => ({
  type: 'GET_MY_SHOWS',
  shows,
});

export const getTopShows = shows => ({
  type: 'GET_TOP_SHOWS',
  shows,
});
