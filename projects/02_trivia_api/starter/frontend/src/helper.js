// get the category name by id from state of categories
function getCategoryById(id, categories) {
    for (let category of categories){
        console.log(category)
        if(parseInt(Object.keys(category)[0]) == id) {
            return Object.values(category)[0]
        }
    }
}

export default getCategoryById