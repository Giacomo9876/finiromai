pragma solidity ^0.8.0;
import "azir_contract.sol";

interface PythonOperations {
    function burned(address add, uint256 amount_to_burn) external view returns (uint256);
}

contract TakeValue {
    PythonOperations public math;
    
    constructor(address takeAddress) {
        takeAddress = PythonOperations(takeAddress);
    }
    
    function burned(address add, uint256 amount_to_burn) external view returns (uint256) {
        return takeAddress.burn(add, amount_to_burn);
    }
}
