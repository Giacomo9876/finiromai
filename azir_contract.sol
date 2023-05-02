pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Azir is ERC20, Ownable {
    
    constructor() ERC20("Azir", "AZR") {
        _mint(msg.sender, 10000000000 * 10 ** decimals());
    }
    
    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        require(recipient != address(0), "Azir: transfer to the zero address");
        require(amount <= balanceOf(msg.sender), "Azir: transfer amount exceeds balance");
        _transfer(_msgSender(), recipient, amount);
        return true;
    }

    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return super.allowance(owner, spender);
    }

    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        require(spender != address(0), "Azir: approve to the zero address");
        require(amount <= balanceOf(msg.sender), "Azir: approve amount exceeds balance");
        _approve(msgSender(), spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public virtual override returns (bool) {
        require(sender != address(0), "Azir: transfer from the zero address");
        require(recipient != address(0), "Azir: transfer to the zero address");
        require(amount <= balanceOf(sender), "Azir: transfer amount exceeds balance");
        require(amount <= allowance(sender, msg.sender), "Azir: transfer amount exceeds allowance");
        _transfer(sender, recipient, amount);
        _approve(sender, msg.sender, allowance(sender, msg.sender) - amount);
        return true;
    }

    function mint(address account, uint256 amount) public onlyOwner {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) public onlyOwner {
        _burn(account, amount);
    }

    function callPythonFunction(string calldata json) external {
        //qui va il codice python
    }
}
