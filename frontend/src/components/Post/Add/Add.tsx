import React, { useState, ChangeEvent, FormEvent } from "react"
import { DropzoneOptions, useDropzone } from "react-dropzone"

import styles from "./Add.module.scss"
import axios from "axios";
import { API_URL } from "../../../services/Api/Api"

export const AddPost = () => {
  const [title, setTitle] = useState<string>("")
  const [description, setDescription] = useState<string>("")
  const [tag, setTag] = useState<string>("")
  const [image, setImage] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault()

    const formData = new FormData()

    formData.append('post', JSON.stringify({ title, description, tag }))

    if (image) {
        formData.append('image', image)
    }

    axios
        .post(API_URL + 'posts/add', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        .then((response) => {
            console.log(response)
        })
        .catch((err) => {
            console.log('Błąd')
        });

    console.log({ title, description, tag, image })
}

  const handleImageChange = (
    e: ChangeEvent<HTMLInputElement>
  ): void => {
    if (e.target.files) {
      setImage(e.target.files[0])
    }
  }

  type CustomDropzoneOptions = Omit<DropzoneOptions, 'accept'> & {
    accept?: string | string[]
  }
  
  const useCustomDropzone = (options: CustomDropzoneOptions) => {
    return useDropzone(options as DropzoneOptions)
  }
  
  const { getRootProps, getInputProps, isDragActive } = useCustomDropzone({
    accept: "image/*",
    multiple: false,
    onDrop: (acceptedFiles) => {
      setImage(acceptedFiles[0])
      setPreviewUrl(URL.createObjectURL(acceptedFiles[0]))
    },
  })

  const dropzoneStyles: React.CSSProperties = {
    borderWidth: "2px",
    borderColor: "#666",
    borderStyle: "dashed",
    borderRadius: "5px",
    padding: "16px",
    textAlign: "center",
  }

  return (
    <>
      <div className={styles.container}>
        <form className={styles.form} onSubmit={handleSubmit}>

          <label className={styles.form__label} htmlFor="title">Tytuł:</label>
          <input
            className={styles.form_input}
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          
          <label className={styles.form__label} htmlFor="description">Opis:</label>
          <textarea
            className={styles.form_textarea}
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <label className={styles.form__label} htmlFor="tag">Tag:</label>
          <input
            className={styles.form_input}
            type="text"
            id="tag"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
          />

          <label className={styles.form__label} htmlFor="image">
            Zdjęcie:
          </label>
          <div
            {...getRootProps()}
            className={`${styles.dropzone} ${
              isDragActive ? styles.form_dragActive : ""
            }`}
          >
            <input {...getInputProps()} id="image" />
            {isDragActive ? (
              <p>Upuść zdjęcie tutaj...</p>
            ) : (
              <p>
                Przeciągnij i upuść zdjęcie tutaj, lub kliknij aby wybrać
                plik.
              </p>
            )}
          </div>

          {previewUrl && (
            <div className={styles.preview}>
              <img src={previewUrl} alt="Podgląd obrazu" />
            </div>
          )}

          <button className={styles.form__submit} type="submit">
            Dodaj post
          </button>
        </form>
      </div>
    </>
  );
};

