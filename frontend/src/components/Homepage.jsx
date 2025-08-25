import React from "react"
import { useParams } from "react-router-dom"

function Homepage() {
    const {familyId} = useParams()

    return (
        <div>
            homepage
        </div>
    )
}

export default Homepage