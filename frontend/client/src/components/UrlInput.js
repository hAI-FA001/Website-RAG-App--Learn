import { useState } from "react";


function UrlInput({ onSubmit }) {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [resMsg, setResMsg] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            // use our backend to upload to Pinecone
            const res = await fetch("http://localhost:5000/embed-and-store", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url })
            })

            if (res.ok) {
                const data = res.json();
                setResMsg(data.message);
                onSubmit()
            } else {
                setResMsg("Error: Something went wrong.")
            }
        } catch (error) {
            console.error("Error: ", error)
            setResMsg("Error: Something went wrong.")
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="urlinput">
            <form onSubmit={handleSubmit}>
            <h1>Start by Providing a URL</h1>
                <input
                    type="text"
                    placeholder="Enter URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Building index..." : "Submit"}
                </button>
            </form>
            {resMsg && <p>{resMsg}</p>}
        </div>
    );
}

export default UrlInput