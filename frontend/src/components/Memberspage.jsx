import React from "react"
import { useParams } from "react-router-dom"
import "../../styles/Memberspage.css"

function Memberspage() {
    const {familyId} = useParams()

    return (
        <div>
            memebrspage
        </div>
    )
}

export default Memberspage