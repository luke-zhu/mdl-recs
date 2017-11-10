import React, { PropTypes } from 'react';
import {
  Card,
  CardTitle,
} from 'material-ui/Card';

const MDLCard = ({ show }) => (
  <Card>
    <CardTitle title={show.name} subtitle={show.myScore} />
  </Card>
);

MDLCard.propTypes = {
  show: PropTypes.object.isRequired,
};

export default MDLCard;
