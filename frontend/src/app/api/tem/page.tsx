import React from 'react'

async function getData() {
  const res = await fetch('http://localhost:8000/api/tem')
  if (!res.ok) {
    throw new Error('failed to fetch data')
  }
  return res.json()
}

export default async function TemPage() {
  const data = await getData()
  return (
    <div>
      hello world
     <p>Status: {data.status}</p>
      <p>Message: {data.message}</p>      
    </div>
  )
};


