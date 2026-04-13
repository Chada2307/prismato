export function createCounter(){
    let count = $state(0);

    return{
        get value() {return count;},
        decrement() { count -= 1},
        increment() { count += 1}
    }
}