import './App.css';
import { storage } from "./firebase";
import { ref, uploadBytesResumable, getDownloadURL, listAll} from "firebase/storage";
import {useState} from "react";

function FirebaseApp() {

	const [uploadedFile, setUploadedFile] = useState(null);
	const [showUpload, setShowUpload] = useState(false);
	const [items, setItems] = useState([]);

	function changeStatus(e){
		setUploadedFile(e.target.files[0]);
	}

	function handleUpload(e){
		e.preventDefault();
		if (uploadedFile === null) return;
		const storageRef = ref(storage, '/files/' + uploadedFile.name);
		const uploadTask = uploadBytesResumable(storageRef, uploadedFile);
		uploadTask.on("state_changed", console.log, console.error, () => {
			getDownloadURL(storageRef)
			  .then((url) => {
				setUploadedFile(null);
				setShowUpload(true);
			  });
		  })
	}

	function listFiles(){
		setItems([]);
		const storageRef = ref(storage, '/files/');
		console.log(storageRef);
		const pullTask = listAll(storageRef)
		pullTask.then(
			(results) => {
				let promises = results.items.forEach(item => getDownloadURL(item).then(url => {
					console.log("heh");
					setItems(arr => [...arr, {ref: item, link : url}]);
				}));
			}
		)
	}

	function downloadFile(url){
		console.log(url);
		window.location.href = url;
	}


	return (
		<div className = "FirebaseApp">
			<input type="file" onChange={changeStatus}/>
			<button onClick={handleUpload}> Upload File </button>
			<h1>{showUpload ?
			<div>
				File uploaded!
			</div> : null} 
			</h1>
			<button onClick={listFiles}>List Item</button>
			<br /><br />
			{
			items.map((val) => (
				<><h2>{val.ref.name}</h2><button onClick={() => downloadFile(val.link)}>
					Download
				</button></>
			))
			}
		</div>

	);

}

export default FirebaseApp;