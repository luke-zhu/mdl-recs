import {List, ListItem} from 'material-ui/List';
import React from 'react';
import {connect} from 'react-redux';

const styles = {
  marginLeft: 24,
};

class HighlightList extends React.Component {
  render() {
    // TODO: 3 review/comment snippets
    if (this.props.selectedShow) {
      const title = this.props.selectedShow._source.main_title;
      return (
          <div style={styles}>
            <h2>{title}</h2>
            <h3>What Others are Saying</h3>
            <List>
              <ListItem>This show sucks.</ListItem>
              <ListItem>Bob is cool.</ListItem>
              <ListItem>Don't watch this.</ListItem>
            </List>
          </div>
      );
    }
    return null;
  }
}

const mapStateToProps = (state) => {
  return {
    selectedShow: state.selectedShow,
  };
};

export default connect(mapStateToProps)(HighlightList);
