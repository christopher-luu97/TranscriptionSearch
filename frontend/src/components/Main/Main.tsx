import React from 'react';
import { Cards } from '../Cards/Cards';
import { Search } from '../Search/Search';

export const Main: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-900">
            <div className="flex items-center justify-center">
                <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
                Search Your Transcripts
                </h1>
            </div>
            <div className="container mx-auto">
                <div className="mb-4">
                    <Search />
                </div>
                <div className="flex items-center justify-between"></div>
                    <Cards></Cards>
            </div>
        </div>
    )
}
