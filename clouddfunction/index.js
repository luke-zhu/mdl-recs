const request = require('request');

/**
 * Redirects any HTTP request to the Elasticsearch server, with parameters
 * included. This function serves to bypass the content security restriction
 * imposed by Github Pages.
 *
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
 */
exports.handleRequest = (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET');
  request('http://35.196.227.212:9200/show/_search' + req.url).pipe(res);
};
