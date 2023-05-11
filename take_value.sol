pragma solidity ^0.8.0;
import "azir_contract.sol";

interface BurnValue {
    function get_token_to_burn_from_lol(uint256 amount_to_burn) external view returns (uint256);
}

contract TakeValue {
    BurnValue public burning_eyes;
    
    constructor(address takeAddress) {
        burning_eyes = BurnValue(takeAddress);
    }
    
    function burned(uint256 amount_to_burn) external view returns (uint256) {
        return burning_eyes.get_token_to_burn_from_lol(amount_to_burn);
    }
}
