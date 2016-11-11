import { Meteor } from 'meteor/meteor';
import { Mongo } from 'meteor/mongo';
import { check } from 'meteor/check';

const Shows = new Mongo.Collection('Shows');

Meteor.methods({
  'shows.getTop': (numShows) => {
    check(numShows, Number);
    return (
      Shows.find({}, {
        sort: { rating: -1 },
        limit: numShows,
      }).fetch()
    );
  },
});

export default Shows;
