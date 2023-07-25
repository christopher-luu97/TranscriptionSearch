import React from 'react';
import './App.css';
import Main from './components/Main/Main'
import { Footer } from './components/Footer/Footer';
import { Header } from './components/Header/Header';

const App: React.FC = () => {
  return (
    <div>
    <Header></Header>
    <Main></Main>
    <Footer></Footer>
    </div>
  );
};

export default App;

