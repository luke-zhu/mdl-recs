import { Meteor } from 'meteor/meteor';
import { HTTP } from 'meteor/http';

Meteor.methods({
  'mdl.getList': username => {
    const content = HTTP
      .get(`http://mydramalist.com/dramalist/${username}`)
      .content;
    const titles = [];

    // Gets the titles and scores
    for (let i = 0; i < content.length; i += 1) {
      if (content.substring(i, i + 6) === 'title=') {
        let t = '';
        let j = 7;
        while (content[i + j] !== '"') {
          t += content[i + j];
          j += 1;
        }
        while (content.substring(i + j, i + j + 6) !== 'score_') {
          j += 1;
        }
        titles.push({
          name: t,
          myScore: content.substring(i + j + 6, i + j + 8) / 10,
        });
      }
    }
    return titles;
  },
});
