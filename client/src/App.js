import { Route, Routes } from 'react-router-dom';

import HomePage from './pages/Home';
import ClassicEA from './pages/ClassicEA';
import Layout from './components/layout/Layout';

const App = () => {
    return (
      <Layout>
        <Routes>
          <Route path='/' exact element={<HomePage />}>
          </Route>    
          <Route path='/classic-EA' exact element={<ClassicEA />}>
          </Route>         
        </Routes>
      </Layout>
    );
}

export default App;