import { update as updateSnake, draw as drawSnake, SNAKE_SPEED, getSnakeHead, snakeIntersection } from './snake.js'
import { update as updateFood, draw as drawFood } from './food.js'
import { outsideGrid } from './grid.js'

const gameBoard = document.getElementById('game-board')
let lastRenderTime = 0
let gameOver = false

function main(currentTime) {
    if (gameOver) {
        if (confirm("You lost. Press ok to restart")) {
            window.location = '/projects/snake_clone/snake.html'
        }
        return
    }

    const secondsSinceLastRender = (currentTime - lastRenderTime)/1000
    window.requestAnimationFrame(main)

    if (secondsSinceLastRender < 1/SNAKE_SPEED) return
    lastRenderTime = currentTime
    update()
    draw()
}

window.requestAnimationFrame(main) //initial first loop


function update() {
    updateSnake()
    updateFood()
    checkDeath()
}

function draw() {
    gameBoard.innerHTML = ''
    drawSnake(gameBoard)
    drawFood(gameBoard)
}

function checkDeath() {
    gameOver = outsideGrid(getSnakeHead()) || snakeIntersection()
}