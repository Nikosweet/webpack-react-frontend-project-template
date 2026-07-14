import { Outlet } from 'react-router-dom'
import classes from '@/components/App.module.scss'

export default function App() {
  return (
  <>
    <main className={classes.main}><Outlet/></main>
  </>
  )
}