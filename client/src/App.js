import { Route, Routes } from 'react-router-dom';

import HomePage from './pages/Home';
import Layout from './components/layout/Layout';

const App = () => {
    return (
      <Layout>
        <Routes>
          <Route path='/' exact element={<HomePage />}>
          </Route>           
        </Routes>
      </Layout>
    );
}

export default App;