import React from 'react';
import './App.css';
import { Cards}  from './components/Main/Main'
import { Footer } from './components/Footer/Footer';
import { Header } from './components/Header/Header';

const App: React.FC = () => {
  return (
    <div>
    <Header></Header>
    <Cards></Cards>
    <Footer></Footer>
    </div>
  );
};

export default App;

