import { createRoot } from 'react-dom/client'
import App from './components/App'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Children } from 'react';
import { Example } from '@/pages/Example';

const root = document.getElementById('root')

if (!root) {
    throw new Error('root not found');
}

const container = createRoot(root);

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            // {
            //     path: '/example',
            //     element: <Example />
            // },
        ]
    }
])

container.render(
    <RouterProvider router={router} />
);