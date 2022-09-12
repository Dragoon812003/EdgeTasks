    //Task View
    const taskItems = document.getElementsByClassName('todo-item')
    const taskView = document.getElementById('task-view')
    const taskViewClose = document.getElementById('task-view-close')
    const taskViewSection1 = document.getElementById('task-view-section-1')
    const taskViewSection2 = document.getElementById('task-view-section-2')
    const taskViewBar = document.getElementById('task-view-bar')

    const taskViewTitle = document.getElementById('task-view-title')
    const taskViewDescription = document.getElementById('task-view-description')
    const taskIdInputs = document.getElementsByClassName('task-id')

    const commentTitle = document.getElementById('comment-title')
    const commentSection = document.getElementById('comment-section')

    const dateOptions = {year: "numeric", month: "short", day: "numeric"}

    for (let i = 0; i < taskItems.length; i++) {
        taskItems[i].addEventListener('click', () => {
            taskView.classList.remove('hidden')
            taskViewSection2.classList.add(`taskview-background-priority-${taskItems[i].dataset.taskPriority}`)
            // taskViewBar.classList.add(`background-priority-${taskItems[i].dataset.taskPriority}`)
            
            for (let j = 0; j < taskIdInputs.length; j++) {
                taskIdInputs[j].setAttribute('value', taskItems[i].dataset.id)
            }


            $.ajax({
                url: "{% url 'task_view' %}",
                type: "POST",
                data: {
                    'task_id': taskItems[i].dataset.id,
                    'user': "{{ request.user }}",
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },

                success: function (data) {
                    $('#task-view-title').text(data.title) 
                    $('#task-view-description').text(data.description)
                    $('#comment-title').text("Comments(" + data.comments.length + ")")
                    $('#task-view-date-added').text(new Date(data.date_added.slice(0, 10)).toLocaleDateString('en-us', dateOptions))

                    $("#edit-title").attr("value", data.title)
                    $("#edit-description").attr("value", data.description)
                    $("#edit-date-time").attr("value", data.date.slice(0, 16))

                    for (let i = data.comments.length - 1; i >= 0; i--) {

                        // <div class="flex py-2">
                        //     <img src="{% static 'images/no_profile.png' %}" class="w-10 h-10 rounded-full m-2">
                        //     <div>
                        //         <div class="px-2"><span class="font-semibold">EdgeTasks</span><span class="font-normal"> on 22 July 2022</span></div>
                        //         <div class="px-2">This is the comment content. I wanted to make this a very long comment so that is why I am typing nonsense here plz ignore this.</div>
                        //     </div>
                        // </div>

                        mainCommentDiv = document.createElement('div')
                        commentSection.appendChild(mainCommentDiv)
                        mainCommentDiv.classList.add("comment-element")
                        mainCommentDiv.classList.add("flex")
                        mainCommentDiv.classList.add("py-2")
                        profilePic = document.createElement('img')
                        profilePic.setAttribute('src', "{% static 'images/no_profile.png' %}")
                        profilePic.classList.add("w-10")
                        profilePic.classList.add("h-10")
                        profilePic.classList.add("rounded-full")
                        profilePic.classList.add("m-2")
                        mainCommentDiv.appendChild(profilePic)
                        commentInfoDiv = document.createElement('div')
                        mainCommentDiv.appendChild(commentInfoDiv)
                        commentInfoDiv.classList.add("px-2")
                        commentAuthorDateDiv = document.createElement('div')
                        commentInfoDiv.appendChild(commentAuthorDateDiv)
                        authorSpan = document.createElement('span')
                        commentAuthorDateDiv.appendChild(authorSpan)
                        authorSpan.classList.add("font-semibold")
                        authorSpan.innerText = data.comments[i].author
                        dateSpan = document.createElement('span')
                        commentAuthorDateDiv.appendChild(dateSpan)
                        dateSpan.classList.add("font-seminormal")
                        dateSpan.innerText = ` on ${new Date(data.comments[i].date.slice(0, 10)).toLocaleDateString('en-us', dateOptions)}`
                        commentContentDiv = document.createElement('div')
                        commentInfoDiv.appendChild(commentContentDiv)
                        commentContentDiv.innerText = data.comments[i].content
                    }

                    // <div data-id="" data-task-priority="" class="todo-item border-2 w-full h-auto my-6 flex p-2 rounded-lg background-priority-{{ todo.priority }} border-priority-{{ todo.priority }}">
                    //     <div class="w-12 flex justify-items-center items-center">
                    //         <input type="checkbox">
                    //     </div>
                    //     <div class="w-87">
                    //         <div class="w-full font-semibold text-2xl priority-{{ todo.priority }}">This is the Subtask title</div>
                    //         <div class="font-light text-sm">due on <span class="font-normal text-base">24 Aug</span></div>
                    //         <div class="w-full font-normal text-lg">This is the description</div>
                    //     </div>
                    // </div>
                    
                    const subTaskView = document.getElementById('sub-task-view')

                    for (let i = data.sub_tasks.length - 1; i >= 0; i--) {
                        mainSubTaskDiv = document.createElement('div')
                        subTaskView.appendChild(mainSubTaskDiv)
                        mainSubTaskDiv.classList.add('todo-item', 'border-2', 'w-full', 'h-auto', 'my-6', 'flex', 'p-2', 'rounded-lg')
                        inputDiv = document.createElement('div')
                        mainSubTaskDiv.appendChild(inputDiv)
                        inputDiv.classList.add('w-12')
                        checkBoxInput = document.createElement('input')
                        checkBoxInput.type = "checkbox"
                        inputDiv.appendChild(checkBoxInput)
                        subTaskContentDiv = document.createElement('div')
                        mainSubTaskDiv.appendChild(subTaskContentDiv)
                        subTaskContentDiv.classList.add('w-87')
                        subTaskTitle = document.createElement('div')
                        subTaskContentDiv.appendChild(subTaskTitle)
                        subTaskTitle.classList.add('w-full', 'font-semibold', 'text-2xl')
                        subTaskTitle.innerText = data.sub_tasks[i].title
                        subTaskDateDiv = document.createElement('div')
                        subTaskContentDiv.appendChild(subTaskDateDiv)
                        subTaskDateDiv.classList.add('font-light', 'text-sm')
                        subTaskDateDiv.innerText = "due on "
                        subTaskDateSpan = document.createElement('div')
                        subTaskDateDiv.appendChild(subTaskDateSpan)
                        subTaskDateSpan.classList.add('font-normal', 'text-base')
                        subTaskDateSpan.innerText = new Date(data.sub_tasks[i].date.slice(0, 10)).toLocaleDateString('en-us', dateOptions)
                        subTaskDescription = document.createElement('div')
                        subTaskContentDiv.appendChild(subTaskDescription)
                        subTaskDescription.classList.add('w-full', 'font-normal', 'text-lg')
                        subTaskDescription.innerText = data.sub_tasks[i].description
                    }
                }
            })
        })
      }

    taskViewClose.addEventListener('click', () => {
        taskView.classList.add('hidden')
        taskViewTitle.innerText = ""
        taskViewDescription.innerText = ""

        commentElem = document.getElementsByClassName('comment-element')
        for (let i = commentElem.length - 1; i >= 0; i--) {
            commentElem[i].parentNode.removeChild(commentElem[i])
        }

        for (let i = 0; i < 4; i++) {
            taskViewSection2.classList.remove(`taskview-background-priority-${i}`)
            // taskViewBar.classList.remove(`background-priority-${i}`)

        }
    })

    editButton = document.getElementById('edit-button')
    taskViewInfo = document.getElementById('task-view-info')
    taskViewEdit = document.getElementById('task-view-edit')
    cancelEditButton = document.getElementById('cancel-edit')

    editButton.addEventListener('click', () => {
        taskViewInfo.classList.add('hidden')
        taskViewEdit.classList.remove('hidden')
    })

    cancelEditButton.addEventListener('click', () => {
        taskViewInfo.classList.remove('hidden')
        taskViewEdit.classList.add('hidden')
    })

    //Subtasks
    const addSubTaskButton = document.getElementById('add-sub-task-button')
    const taskViewSubSection = document.getElementById('task-view-sub-section')
    const addSubTask = document.getElementById('add-sub-task')
    const addSubTaskCancel = document.getElementById('add-sub-task-cancel')
    
    addSubTaskButton.addEventListener('click', () => {
        addSubTaskButton.classList.add('hidden')
        addSubTask.classList.remove('hidden')
    })

    addSubTaskCancel.addEventListener('click', () => {
        addSubTask.classList.add('hidden')
        addSubTaskButton.classList.remove('hidden')
    })