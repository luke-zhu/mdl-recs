import List, {ListItem} from 'material-ui/List';
import Divider from 'material-ui/Divider';
import React from 'react';
import {connect} from 'react-redux';

const styles = {
  margin: 20,
};

class HighlightList extends React.Component {
  render() {
    if (this.props.selectedShow) {
      console.log(this.props.selectedShow);
      const title = this.props.selectedShow._source.main_title;
      let highlights = [];
      if (this.props.selectedShow._source.highlights) {
        highlights = this.props.selectedShow._source.highlights;
      }
      const listItems = highlights.slice(0, 3).map((e, i) => {
        return <div><ListItem key={i}>{e}</ListItem><Divider/></div>;
      });
      return (
          <div style={styles}>
            <h2>{title}</h2>
            <h3>Review Snippets</h3>
            <List>
              {listItems}
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
