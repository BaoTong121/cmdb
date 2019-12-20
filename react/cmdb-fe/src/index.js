import React from 'react';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import Getip from './component/Getip';

function Home() {
  return (
    <div>
      <h2>Home</h2>
    </div>
  );
}


 function Root() {
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/ip">get ip</Link>
          </li>
        </ul>
        <hr />
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/ip">
            <Getip  />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}


ReactDOM.render(<Root />, document.getElementById('root'));