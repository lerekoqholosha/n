
import streamlit as st
from dataclasses import dataclass
counter=0
def next(): st.session_state.counter += 1
def prev(): st.session_state.counter -= 1
if 'counter' not in st.session_state: st.session_state.counter = 0

questions=['what is your first name','what is your last name']
@dataclass
class AnnotatedImage():
    '''
    Dataclass to store an image with an id and an annotation
    Data class Display next questions when someone clicks
    '''
    id: int
    annotation = ""
   
    def __post_init__(self):
        #self.url = f"https://dummyimage.com/600x200/000/fff&text=IMAGE_{self.id}"
        self.questions=questions

def main():

    # Load images and the current annotations
    if "my_images" not in st.session_state:
        my_images = [AnnotatedImage(id=i) for i in range(5)]
        st.session_state.my_images = my_images

    else:
        my_images = st.session_state.my_images

    n_imgs = len(my_images)

    # App layout
    container = st.empty()
    cols = st.columns(2)
    with cols[1]: st.button("Next ", on_click=next, use_container_width=True)
    with cols[0]: st.button(" Previous", on_click=prev, use_container_width=True)    
   
    # Fill layout
    with container.container():
        ## Select image based on the current counter
        img = my_images[st.session_state.counter%n_imgs]

        ## Display image
        st.image(img.url, use_column_width=True)
       
        ## Get annotation from text_area and allow modification
        text = st.text_area(f"Insert annotation for image {img.id}:", value=img.annotation)
        img.annotation = text

    # Show state of changes
    with st.sidebar:
        "****"
        "### Debug"
        f" `{st.session_state.counter=}`"
        st.table({img.id : img.annotation for img in my_images})

if __name__ == "__main__":
    main()