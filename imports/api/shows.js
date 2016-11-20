import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

const Shows = new Mongo.Collection('shows');

Meteor.methods({
  'shows.getTop': (numShows) => {
    check(numShows, Number);
    return (
      Shows.find({ average_score: { $gt: 8.5 } }, {
        sort: { num_scores: -1 },
        limit: numShows,
      }).fetch()
    );
  },
});

export default Shows;
