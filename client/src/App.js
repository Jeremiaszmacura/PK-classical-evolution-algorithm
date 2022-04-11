import { Route, Routes } from 'react-router-dom';

import HomePage from './pages/Home';
import ClassicEA from './pages/ClassicEA';
import RealChromosomeEA from './pages/RealChromosomeEA';
import Layout from './components/layout/Layout';

const App = () => {
    return (
      <Layout>
        <Routes>
          <Route path='/' exact element={<HomePage />}>
          </Route>    
          <Route path='/classic-EA' exact element={<ClassicEA />}>
          </Route>     
          <Route path='/real-chromosome-EA' exact element={<RealChromosomeEA />}>
          </Route>    
        </Routes>
      </Layout>
    );
}

export default App;